'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { getReport } from '@/api'
import Link from 'next/link'
import ReportInformation from '@/components/ReportInformation/ReportInformation'
import ReportHeaders from '@/components/ReportHeaders/ReportHeaders'


export default function ReportDetail() {
	const params = useParams()
	const reportId = params.reportId

	const [reportData, setReportData] = useState(null)
	const [headerData, setHeaderData] = useState(null)
	const [sslData, setSslData] = useState(null)
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState(null)

	useEffect(() => {
		const processHeaders = (headers) => {
			const correctHeadersCount = headers.filter(header => 
				header.correct && header.enabled
				|| header.name === "Refresh" && !header.enabled
			).length;
			const totalHeadersCount = headers.length

			setHeaderData({
				headers: headers,
				correct: correctHeadersCount,
				total: totalHeadersCount,
				percentage: ((correctHeadersCount / totalHeadersCount) * 100).toFixed
			})
		}

		const processSsl = (sslInfo) => {
			if (!sslInfo || sslInfo.error) return

			const startFormattedDate = `${sslInfo.not_before.substring(0, 4)}-${sslInfo.not_before.substring(4, 6)}-${sslInfo.not_before.substring(6, 8)}T${sslInfo.not_before.substring(8, 10)}:${sslInfo.not_before.substring(10, 12)}:${sslInfo.not_before.substring(12, 14)}Z`
			const endFormattedDate = `${sslInfo.not_after.substring(0, 4)}-${sslInfo.not_after.substring(4, 6)}-${sslInfo.not_after.substring(6, 8)}T${sslInfo.not_after.substring(8, 10)}:${sslInfo.not_after.substring(10, 12)}:${sslInfo.not_after.substring(12, 14)}Z`
			const startDate = new Date(startFormattedDate)
			const endDate = new Date(endFormattedDate)
			const daysDifference = (endDate - startDate) / (1000 * 3600 * 24)

			setSslData({
				"Sujeto": sslInfo.subject.CN,
				"Emisor": `${sslInfo.issuer.O} (${sslInfo.issuer.CN})`,
				"Páis": sslInfo.issuer.C,
				"Válidos desde": startFormattedDate,
				"Válido hasta": endFormattedDate,
				"Días restantes": `${Math.floor(daysDifference)} días`,
				"Versión TLS": sslInfo.tls_version,
				"Cifrado TLS": sslInfo.tls_cipher,
			})
		}

		const getReportDetail = async () => {
			try {
				const response = await getReport(reportId)

				if (response.status == 200) {
					const report = response.data.report

					setReportData(report)
					processSsl(report.ssl_info)
					processHeaders([report.hsts, report.csp, report.xframe, report.content_type, report.cookie, report.cache, report.xss, report.referrer, report.permissions, report.refresh])
				}
				else {
					console.error("Error fetching report " + reportId)
					setError(`Error al cargar el informe ${reportId} o informe no existente.`)
				}
			} catch (err) {
				console.error("Error fetching report:", err)
				setError(err.message)
			} finally {
				setLoading(false)
			}
		}

		getReportDetail()
	}, [reportId])

	return (
		<div className="page page-report">
			<div className="container">
				{loading ? (
					<div className="loading">Cargando informe...</div>
				) : (error ? (
					<div className="error">Error al cargar el informe: {error}</div>
				) : (!reportData || !headerData ? (
					<div className="error">No se encontraron datos del informe.</div>
				) : (<>
					<section className="report-hero">
						<div className="card">
							<div className="card-header">
								<div className="header-content">
									<h1 className="report-title ptext">Resumen del informe</h1>
									<p className="report-subtitle stext">Informe generado por webscavul</p>
								</div>
								<div className="chip chip--regular">
									<span className="chip-text"><strong>Informe ID:</strong> {reportId}</span>
								</div>
							</div>
							<ul className="card-body inner">
								<li className="info-item">
									<p className="label stext">Dominio</p>
									<a
										className="value ptext"
										href={reportData.domain.split("/")[0]}
										target="_blank" rel="noopener noreferer"
									>
										{reportData.domain.split("/")[0]}
									</a>
								</li>
								<li className="info-item">
									<p className="label stext">Protocolo</p>
									<p className="value ptext">{reportData.protocol}</p>
								</li>
								<li className="info-item">
									<p className="label stext">Dirección IP</p>
									<div className="valueip">
										{reportData.ip ? (
											reportData.ip.map((ip, index) => (
												<a
													key={index}
													className="value ptext"
													href={`//${ip}`}
													target="_blank" rel="noopener noreferer"
												>
													{ip}
												</a>
											))) : (
											<span>No disponible</span>
										)}
									</div>
								</li>
								<li className="info-item">
									<p className="label stext">Fecha</p>
									<p className="value ptext">{reportData.created_at.split("T")[0].split("-").reverse().join("/")}</p>
								</li>
							</ul>
							<div className="card-buttons">
								<Link
									href={`/reports`}
									className="button button-primary"
								>
									Mis informes
								</Link>
								<Link
									href="/"
									className="button button-secondary"
								>
									Nuevo informe
								</Link>
							</div>
						</div>
						<ul className="resume-list">
							{reportData.type === "full" && (
								<li className="card resume-card">
									<h3 className="resume-title">Vulnerabilidades</h3>
									<p className="resume-value">{reportData.vulnerabilities} vulnerabilidades encontradas</p>
									<div className="resume-buttons">
										<Link
											href={`/report/${reportId}/board`}
											className="button button-primary"
										>
											Ver tablero
										</Link>
									</div>
								</li>
							)}
							<li className="card resume-card">
								<h3 className="resume-title">Cabeceras</h3>
								<p className="resume-value">{headerData.correct} / {headerData.total} cabeceras configuradas</p>
							</li>
							<li className="card resume-card">
								<h3 className="resume-title">SSL</h3>
								<p className="resume-value">
									{sslData ? (
										"SSL configurado correctamente"
									) : (
										"SSL no configurado"
									)}
								</p>
							</li>
						</ul>
					</section>
					<ReportInformation
						reportData={reportData}
						sslData={sslData}
					/>
					<ReportHeaders
						headerData={headerData}
					/>
				</>)))}
			</div>
		</div>
	)
} 