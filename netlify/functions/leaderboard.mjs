export default async () => {
  return new Response(
    JSON.stringify({
      ok: true,
      message: "Leaderboard-funktio toimii"
    }),
    {
      status: 200,
      headers: {
        "Content-Type": "application/json"
      }
    }
  );
};