"use client"

import { redirect } from 'next/navigation'

import InputURL from "@/components/InputDomain/InputDomain"
import { createReport } from "@api"

export default function Home() {
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
		console.log("Escaneando " + domain)

		if (isValidDomain(domain)) {
			const response = await createReport(domain)

			if (response.status == 200) {
				const reportId = response.data.report_id
				// TODO - Show a success modal or smth
				redirect(`/report/${reportId}`)
			}

			// TODO - Handle error
		}
		else {
			// TODO - Mostrar error
			console.log("DOMINIO NO VALIDO")
		}
	}

	return (
		<div className="page page-home">
			<section className="scan-hero">
				<div className="container">
					<div className="hero-content">
						<h1 className="text-xxl">WEBSCAVUL - Full Scan</h1>
						<p className="text-md">Encuentra fallos y vulnerabilidades en tu página web, solo con introducir la URL.</p>
					</div>
					<div className="scanner-card">
						<InputURL onSubmitScan={handleScan} />
					</div>
				</div>
			</section>
			<section className="home-info">
				<div className="container">
					
				</div>
			</section>
		</div>
	);
}
