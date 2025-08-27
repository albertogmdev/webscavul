import Groq from "groq-sdk";

const groq = new Groq({
	apiKey: process.env.NEXT_PUBLIC_API_KEY,
});

export async function askAI(query) {
	try {
		const response = await groq.chat.completions.create({
			model: "llama-3.3-70b-versatile",
			messages: [
				{ role: "system", content: "Eres un asistente que explica vulnerabilidades y da soluciones técnicas claras." },
				{ role: "user", content: query }
			],
		});

		return response.choices[0].message.content;
	} catch (error) {
		console.error("Error consultando AI:", error);
		throw error;
	}
}