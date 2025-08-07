'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { getReport } from '@/api'


export default function ReportDetail() {
	const params = useParams()
	const reportId = params.reportId
	const [reportData, setReportData] = useState(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);

	useEffect(() => {
		const getReportDetail = async () => {
			try {
				const data = await getReport(reportId)
				setReportData(data.data.report)
				console.log(data)
			} catch (err) {
				setError(err.message)
			} finally {
				setLoading(false)
			}
		}

		getReportDetail()
	}, [reportId])

	if (loading) return <p>Loading report...</p>
	if (error) return <p>Error loading report: {error}</p>
	if (!reportData) return <p>Report not found.</p>

	return (
		<div className="page page-report}">
			<section className="report-hero">
				<div className="container">
					
				</div>
			</section>
		</div>
	)
} 