"use client"

import { useEffect, useState } from 'react'
import { getAllReports, deleteReport } from '@/api'
import Link from 'next/link'
import Reportlist from '@/components/ReportList/ReportList'

export default function Reports() {
	const [reportData, setReportData] = useState(null)
	const [filteredReportData, setFilteredReportData] = useState(null)
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState(null)

	useEffect(() => {
		const getAllReportsData = async () => {
			try {
				const response = await getAllReports()

				if (response.status === 200) {
					const reports = response.data.reports
					
					setReportData(reports)
					setFilteredReportData(reports)
				}
				else setError(`Error fetching reports: ${response.error}`)
			} catch (err) {
				setError(`Failed to fetch reports: ${err.message}`)
			} finally {
				setLoading(false)
			}
		}

		getAllReportsData()
	}, [])

	const handleReportDelete = async (reportId) => {
		try {
			const response = await deleteReport(reportId)

			if (response.status === 200) {
				const afterDelete = reportData.filter(report => report.id !== reportId)

				setReportData(afterDelete)
				setFilteredReportData(afterDelete)	
				return true
			}
			else {
				console.error("Error deleting report")
				return false
			}
		} catch (err) {
			console.error("Error deleting report")
			return false
		}
	}

	return (
		<div className="page page-reports_list">
			<div className="container">
				{loading ? (
					<div className="loading">Cargando informes...</div>
				) : error ? (
					<div className="error">Error al cargar los informes: {error}</div>
				) : !reportData ? (
					<div className="error">No se encontraron informes.</div>
				) : (<>
					<section className="reports-hero">
						<div className="card">
							<div className="card-header">
								<div className="header-content">
									<h1 className="report-title ptext">Informes generados</h1>
									<p className="report-subtitle stext">Visualiza y gestiona los informes generados por Webscavul</p>
								</div>
								<Link href="/" className="button button-primary">
									Nuevo escaneo
								</Link>
							</div>
						</div>
					</section>
					<Reportlist 
						reportData={filteredReportData} 
						onDeleteReport={handleReportDelete}
					/>
				</>)}
			</div>
		</div>
	)
}
