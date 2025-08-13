'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { getReport } from '@/api'
import Link from 'next/link'


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
			const correctHeadersCount = headers.filter(header => header.correct && header.enabled).length;
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

		const processGeneralInfo = (generalInfo) => {

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
					console.error("Error fetching report "+ reportId)
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
									<p className="value ptext">{reportData.domain}</p>
								</li>
								<li className="info-item">
									<p className="label stext">Protocolo</p>
									<p className="value ptext">{reportData.protocol}</p>
								</li>
								<li className="info-item">
									<p className="label stext">Dirección IP</p>
									<p className="value ptext">192.168.0.0</p>
								</li>
								<li className="info-item">
									<p className="label stext">Fecha</p>
									<p className="value ptext">{reportData.date}</p>
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
					<section className="report-information">
						<div className="card">
							<h2 className="card-title">Información general y certificado SSL</h2>
							<div className="information-content">
								<div className="content-col general-info">
									<ul className="info-table">
										<h3 className="table-header">Información general</h3>
										<li className="table-item">
											<h4 className="label stext">Dominio</h4>
											<p className="value ptext">{reportData.domain}</p>
										</li>
										<li className="table-item">
											<h4 className="label stext">URL</h4>
											<p className="value ptext">{reportData.full_domain}</p>
										</li>
										<li className="table-item">
											<h4 className="label stext">Dirección IP</h4>
											<p className="value ptext">{reportData.ip}</p>
										</li>
										<li className="table-item">
											<h4 className="label stext">Protocolo</h4>
											<p className="value ptext">{reportData.protocol}</p>
										</li>
									</ul>
								</div>
								<div className="content-col ssl-info">
									{sslData ? (
										<ul className="info-table">
											<h3 className="table-header">SSL y TLS</h3>
											{sslData && Object.entries(sslData).map(([key, value]) => (
												<li key={key} className="table-item">
													<h4 className="label stext">{key}</h4>
													<p className="value ptext">{value}</p>
												</li>
											))}
										</ul>
									) : (
										<div className="ssl-error">
											<p className="error-text">No se pudo obtener información del certificado SSL.</p>
											<p className="error-details">Asegúrate de que el sitio web tenga un certificado SSL válido.</p>
										</div>
									)}
								</div>
							</div>
						</div>
					</section>
					<section className="report-headers">
						<div className="card">
							<h2 className="card-title">Análisis de cabeceras HTTP</h2>
							<ul className="headers-list">
								{headerData && headerData.headers && headerData.headers.length > 0 && (
									headerData.headers.map((header, index) => (
										<li key={index} className="header-item">
											<div className="item-content">
												<h3 className="item-title">{header.name}</h3>
												<p className="item-description stext">{header.description}</p>
												{header.value && (<div className="item-value">{[].concat(header.value).join("; ")}</div>)}
											</div>
											<div className="item-chip">
												{header.correct && header.enabled ? (
													<div className="chip chip--success">
														<span className="chip-text">Implementado</span>
													</div>
												) : (header.severity === "warning" ? (
													<div className="chip chip--warning">
														<span className="chip-text">Warning</span>
													</div>
												) : (header.severity === "recommendation" || header.severity === "info" ? (
													<div className="chip chip--info">
														<span className="chip-text">Recomendado</span>
													</div>
												) : (
													<div className="chip chip--error">
														<span className="chip-text">Crítico</span>
													</div>
												)))}
											</div>
										</li>
									))
								)}
							</ul>
						</div>
					</section>
				</>)))}
			</div>
		</div>
	)
} 