export default async () => {
  return new Response(
    JSON.stringify({ ok: true, message: "Netlify Functions toimii" }),
    {
      status: 200,
      headers: { "Content-Type": "application/json" }
    }
  );
};