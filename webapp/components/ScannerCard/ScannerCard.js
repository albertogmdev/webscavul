"use client"

import { useState } from 'react';
import { redirect } from 'next/navigation'
import { createReport } from "@api"
import InputDomain from "@/components/InputDomain/InputDomain"

export default function ScannerCard() {
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
        <div className="scanner-card">
            <InputDomain onSubmitScan={handleScan} />
            {/* <div className="scanner-config">
                <p className="config-title">Configuración</p>
            </div>
            <div className="scanner-others">

            </div> */}
        </div>
    )
}