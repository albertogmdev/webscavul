"use client"

import { useEffect, useState } from 'react'
import { getAllReports, deleteReport } from '@/api'
import Link from 'next/link'
import ReportList from '@/components/ReportList/ReportList'
import ReportFilter from '@/components/ReportFilter/ReportFilter'

export default function Reports() {
	const [reportData, setReportData] = useState(null)
	const [filteredReportData, setFilteredReportData] = useState(null)
	const [filterName, setFilterName] = useState("")
	const [filterType, setFilterType] = useState("")
	const [filterOrder, setFilterOrder] = useState("")
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
		document.title = "Listado de informes | WebScavul"
	}, [])

	const handleReportDelete = async (reportId) => {
		try {
			const response = await deleteReport(reportId)

			if (response.status === 200) {
				const afterDelete = reportData.filter(report => report.id !== reportId)

				setReportData(afterDelete)
				setFilteredReportData(afterDelete)
				// When modifying the board data, we also need to apply the current filters
				applyFilters(filterName, filterType, filterOrder, afterDelete)
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

	const handleFilter = (type, value) => {
		if (type === "name") setFilterName(value.toLowerCase())
		if (type === "type") setFilterType(value.toLowerCase())
		if (type === "order") setFilterOrder(value.toLowerCase())

		const nameData = type === "name" ? value.toLowerCase() : filterName.toLowerCase()
		const typeData = type === "type" ? value.toLowerCase() : filterType.toLowerCase()
		const orderData = type === "order" ? value.toLowerCase() : filterOrder.toLowerCase()
		applyFilters(nameData, typeData, orderData, reportData)
	}

	const applyFilters = (nameData, typeData, orderData, data) => {
		let newReportData = [...data]

		if (nameData !== "") newReportData = newReportData.filter(report => report.full_domain.toLowerCase().includes(nameData))

		if (typeData !== "") newReportData = newReportData.filter(report => report.type.toLowerCase() === typeData)

		if (orderData !== "") {
			if (orderData === "date_asc") newReportData.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
			else if (orderData === "date_desc") newReportData.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
		}

		setFilteredReportData(newReportData)
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
						<ReportFilter
							onFilter={handleFilter}
						/>
					</section>
					<ReportList
						reportCount={reportData.length}
						reportData={filteredReportData}
						onDeleteReport={handleReportDelete}
					/>
				</>)}
			</div>
		</div>
	)
}
