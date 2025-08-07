"use client"

import { useEffect, useState } from "react";

export default function Home() {
	const [data, setData] = useState(null)
    const [error, setError] = useState(null)

	useEffect(() => {
		
	}, [])

	return (
		<div className="">
			<pre>{JSON.stringify(data)}</pre>
		</div>
	);
}
