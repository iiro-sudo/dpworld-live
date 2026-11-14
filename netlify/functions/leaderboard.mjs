export default async () => {
  return new Response(JSON.stringify({
    ok: true,
    mode: "snapshot",
    date: "2026-11-14",
    round: 3,
    message: "Vahvistettu 54 reiän tilanne. Automaattista ulkoista live-lähdettä ei ole vielä käytössä."
  }), {
    status: 200,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store"
    }
  });
};