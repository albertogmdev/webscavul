"use client"

import { useEffect, useState } from "react";

export default function Home() {
	const [data, setData] = useState(null)
    const [error, setError] = useState(null)

	useEffect(() => {
		const fetchData = async () => {
			try {
				const apiUrl = 'http://localhost:8000/analyze?domain=googl.com';

				const response = await fetch(apiUrl);

				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}

				const result = await response.json(); // Parse the JSON response
				setData(result); // Set the fetched data to state

			} catch (e) {
				// Catch any errors during the fetch operation
				console.error("Error fetching data:", e);
				setError(e); // Set the error to state
			}
		};
		
		console.log("hola")
		fetchData()
	}, [])

	return (
		<div className="">

		</div>
	);
}
