"use client"

import Image from "next/image";
import styles from "../page.module.css";
import { useEffect, useState } from "react";

export default function Home() {
	const [data, setData] = useState(null)
    const [error, setError] = useState(null)

	useEffect(() => {
		const fetchData = async () => {
			try {
				const apiUrl = 'http://localhost:8000/report/dd82ac2fe1b93d9258b65ccfc2e7a64ea7c94591a9859421dcd7f906d50f0455/board';

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
		<div className={styles.page}>
			<main className={styles.main}>
				<h1>THIS THE REPORT</h1>
				<pre>{JSON.stringify(data, null, 2)}</pre> 
			</main>
			<footer className={styles.footer}>
				<a
					href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
					target="_blank"
					rel="noopener noreferrer"
				>
					<Image
						aria-hidden
						src="/file.svg"
						alt="File icon"
						width={16}
						height={16}
					/>
					Learn
				</a>
				<a
					href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
					target="_blank"
					rel="noopener noreferrer"
				>
					<Image
						aria-hidden
						src="/window.svg"
						alt="Window icon"
						width={16}
						height={16}
					/>
					Examples
				</a>
				<a
					href="https://nextjs.org?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
					target="_blank"
					rel="noopener noreferrer"
				>
					<Image
						aria-hidden
						src="/globe.svg"
						alt="Globe icon"
						width={16}
						height={16}
					/>
					Go to nextjs.org →
				</a>
			</footer>
		</div>
	);
}
