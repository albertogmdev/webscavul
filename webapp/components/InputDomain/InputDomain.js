"use client"

import { useState } from 'react';

export default function InputURL({onSubmitScan}) {
	const [domain, setDomain] = useState('');

	const handleSubmit = (event) => {
        event.preventDefault()
        if (onSubmitScan) onSubmitScan(domain)
    }

    const handleChange = (event) => { setDomain(event.target.value) }

	return (
		<form className="input-domain" onSubmit={handleSubmit}>
            <input 
				onChange={handleChange}
				className="input-text text-md"
				type="text"
			/>
            <button 
				className="input-submit"
				type="submit"
			>
				Escanear
			</button>
		</form>
	)
}