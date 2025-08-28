"use client"

import { useState } from 'react';
import { useRouter } from 'next/navigation'
import { createReport } from "@api"
import InputDomain from "@/components/InputDomain/InputDomain"

export default function ScannerCard() {
	const [loading, setLoading] = useState(false)
	const [scanType, setScanType] = useState("full")
	const [error, setError] = useState(null)
	const router = useRouter()

	const isValidDomain = (domain) => {
		const regex = new RegExp(
			'^(?:https?://)?' +
			'(?:localhost(?:\\:\\d+)?' +
			'|(?:[a-zA-Z0-9\\-]+\\.)+[a-zA-Z]{2,})' +
			'(?:\\:\\d+)?' +
			'(?:/.*)?$',
			'i'
		)

		return domain !== null && regex.test(domain)
	}

	const handleScan = async (domain) => {
		console.log("Scanning domain:", domain)
		setLoading(true)

		try {
			if (isValidDomain(domain)) {
				const response = await createReport(domain, scanType)
				if (response.status == 200) {
					const reportId = response.data.report_id
					router.push(`/report/${reportId}`)
				}
				else {
					setError("Ha ocurrido un error al crear el informe. Por favor, inténtalo de nuevo.")
					setLoading(false)
				}
			}
			else {
				setError("El dominio introducido no es válido. Por favor, inténtalo de nuevo. Ejemplo: https://example.com")
				setLoading(false)
			}
		}
		catch (error) {
			setError("Ha ocurrido un error al crear el informe. Por favor, inténtalo de nuevo.")
			setLoading(false)
		}
	}

	return (
		<div className={`scanner-card${error ? " scanner-error" : ""}`}>
			{loading && (
				<div className="loading-layout">
					<div className="spinner"></div>
					<div className="loading-text ptext">Escaneando dominio...</div>
				</div>
			)}
			<InputDomain
				onSubmitScan={handleScan}
				onChangeInput={() => { setError(null) }}
			/>
			{error &&
				<p className="error-message">{error}</p>
			}
			<div className="scanner-type">
				<p className="type-title">Tipo de escaneo</p>
				<div className="type-options">
					<div className="type-option">
						<input
							type="radio"
							id="full"
							name="scan-type"
							value="full"
							defaultChecked
							onChange={(e) => { setScanType(e.target.value) }}
						/>
						<label htmlFor="full" className="stext">Completo</label>
					</div>
					<div className="type-option">
						<input
							type="radio"
							id="headers"
							name="scan-type"
							value="headers"
							onChange={(e) => { setScanType(e.target.value) }}
						/>
						<label htmlFor="headers" className="stext">Cabeceras</label>
					</div>
				</div>
			</div>
		</div>
	)
}