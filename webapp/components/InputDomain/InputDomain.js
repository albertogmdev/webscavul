"use client"

import { useState } from 'react';

export default function InputDomain({onSubmitScan}) {
	const [domain, setDomain] = useState('');

	const handleSubmit = (event) => {
        event.preventDefault()
        if (onSubmitScan) onSubmitScan(domain)
    }

    const handleChange = (event) => { setDomain(event.target.value) }

	return (<>
		<p className="input-label" htmlFor="domain">Introduce la URL de la web</p>
		<form className="input-domain" onSubmit={handleSubmit}>
			<input 
				id="domain"
				onChange={handleChange}
				className="input-text"
				type="text"
				placeholder="https://example.com o example.com"
			/>
			<button 
				className="input-submit button button-primary"
				type="submit"
			>
				Escanear
			</button>
		</form>
	</>)
}