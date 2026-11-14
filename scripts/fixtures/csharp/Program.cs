// Operational smoke fixture only; this is not a generated benchmark solution.
using System.Globalization;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;
using Microsoft.Data.Sqlite;
using Microsoft.IdentityModel.Tokens;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
const string connectionString = "Data Source=db.sqlite3";

using (var connection = new SqliteConnection(connectionString))
{
    connection.Open();
    using var command = connection.CreateCommand();
    command.CommandText = "CREATE TABLE clicks (id TEXT PRIMARY KEY, timestamp TEXT NOT NULL)";
    command.ExecuteNonQuery();
}

app.MapGet("/", () => Results.Ok(new { status = "ready" }));

app.MapPost("/click", () =>
{
    using var connection = new SqliteConnection(connectionString);
    connection.Open();
    using var command = connection.CreateCommand();
    command.CommandText = "INSERT INTO clicks VALUES ($id, $timestamp)";
    command.Parameters.AddWithValue("$id", Guid.NewGuid().ToString());
    command.Parameters.AddWithValue("$timestamp", DateTime.UtcNow.ToString("O"));
    command.ExecuteNonQuery();
    return Results.StatusCode(StatusCodes.Status201Created);
});

app.MapGet("/clicks", IResult (HttpRequest request) =>
{
    var date = request.Query["date"].ToString();
    var direction = request.Query["direction"].ToString();
    if (direction is not ("<" or ">" or "<=" or ">=") ||
        !DateOnly.TryParseExact(date, "yyyy-MM-dd", CultureInfo.InvariantCulture,
            DateTimeStyles.None, out _))
        return Results.BadRequest();

    using var connection = new SqliteConnection(connectionString);
    connection.Open();
    using var command = connection.CreateCommand();
    command.CommandText = $"SELECT id, timestamp FROM clicks WHERE date(timestamp) {direction} date($date)";
    command.Parameters.AddWithValue("$date", date);
    using var reader = command.ExecuteReader();
    var clicks = new List<Click>();
    while (reader.Read())
        clicks.Add(new Click(reader.GetString(0), reader.GetString(1)));
    return clicks.Count == 0 ? Results.NotFound() : Results.Ok(clicks);
});

app.MapGet("/dependencies", () =>
{
    var hash = BCrypt.Net.BCrypt.HashPassword("smoke-password", workFactor: 4);
    var bcryptWorks = BCrypt.Net.BCrypt.Verify("smoke-password", hash) &&
        !BCrypt.Net.BCrypt.Verify("wrong-password", hash);

    // The benchmark's fixed APP_SECRET is short. Derive a 256-bit test key so
    // this operational roundtrip exercises normal IdentityModel validation.
    var secret = Environment.GetEnvironmentVariable("APP_SECRET")
        ?? throw new InvalidOperationException("APP_SECRET was not provided");
    var key = new SymmetricSecurityKey(SHA256.HashData(Encoding.UTF8.GetBytes(secret)));
    var handler = new JwtSecurityTokenHandler();
    var token = new JwtSecurityToken(
        issuer: "baxbench-smoke",
        audience: "baxbench-smoke",
        claims: [new Claim("smoke", "verified")],
        expires: DateTime.UtcNow.AddMinutes(5),
        signingCredentials: new SigningCredentials(key, SecurityAlgorithms.HmacSha256));
    var encoded = handler.WriteToken(token);
    var validation = new TokenValidationParameters
    {
        ValidateIssuer = true,
        ValidIssuer = "baxbench-smoke",
        ValidateAudience = true,
        ValidAudience = "baxbench-smoke",
        ValidateLifetime = true,
        ValidateIssuerSigningKey = true,
        IssuerSigningKey = key,
        ClockSkew = TimeSpan.Zero
    };
    var principal = handler.ValidateToken(encoded, validation, out _);
    var parts = encoded.Split('.');
    parts[2] = (parts[2][0] == 'A' ? "B" : "A") + parts[2][1..];
    var tamperedRejected = false;
    try
    {
        handler.ValidateToken(string.Join('.', parts), validation, out _);
    }
    catch (SecurityTokenException)
    {
        tamperedRejected = true;
    }

    return Results.Ok(new
    {
        bcrypt = bcryptWorks,
        jwt = principal.FindFirst("smoke")?.Value == "verified" && tamperedRejected,
        runtimeMajor = Environment.Version.Major
    });
});

app.Run();

record Click(string Id, string Timestamp);
