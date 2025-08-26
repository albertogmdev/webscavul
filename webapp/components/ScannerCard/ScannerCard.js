"use client"

import { useState } from 'react';
import { useRouter } from 'next/navigation'
import { createReport } from "@api"
import InputDomain from "@/components/InputDomain/InputDomain"

export default function ScannerCard() {
	const [loading, setLoading] = useState(false)
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
				const response = await createReport(domain)
				if (response.status == 200) {
					const reportId = response.data.report_id
					router.push(`/report/${reportId}`)
				}
				else {
					// TODO - Mostrar error
					console.log("DOMINIO NO VALIDO")
					setLoading(false)
				}
			}
			else {
				// TODO - Mostrar error
				console.log("DOMINIO NO VALIDO")
				setLoading(false)
			}
		}
		catch (error) {
			// TODO - Mostrar error
			console.error("Error creating report:", error)
			setLoading(false)
		}
	}

	return (
		<div className="scanner-card">
			{loading && (
				<div className="loading-layout">
					<div className="spinner"></div>
					<div className="loading-text ptext">Escaneando dominio...</div>
				</div>
			)}
			<InputDomain onSubmitScan={handleScan} />
			{/* <div className="scanner-config">
                <p className="config-title">Configuración</p>
            </div>
            <div className="scanner-others">

            </div> */}
		</div>
	)
}