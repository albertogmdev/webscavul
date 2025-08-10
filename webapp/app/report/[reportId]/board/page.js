"use client"

import { useParams } from 'next/navigation'
import { useEffect, useState } from "react"
import { getReportBoard } from '@/api'

export default function ReportBoard() {
	const params = useParams()
	const reportId = params.reportId

	const [boardData, setBoardData] = useState(null)
	const [error, setError] = useState(null)
	const [loading, setLoading] = useState(null)

	useEffect(() => {
		const getBoardInfo = async () => {
			try {
				const response = await getReportBoard(reportId)
				const board = response.data.board

				setBoardData(board)
			} catch (err) {
				console.error("Error fetching report:", err)
				setError(err.message)
			} finally {
				setLoading(false)
			}
		}

		getBoardInfo()
	}, [reportId])

	return (
		<div className="page page-board">
			<div className="container">
				{loading ? (
					<div className="loading">Cargando informe...</div>
				) : (error ? (
					<div className="error">Error al cargar el informe: {error}</div>
				) : (!boardData ? (
					<div className="error">No se encontraron datos del tablero del informe.</div>
				) : (<>
					<section className="board-hero">
						<div className="card">
							<div className="card-header">
								<div className="header-content">
									<h1 className="report-title ptext">Tablero de vulnerabilidades</h1>
									<p className="report-subtitle stext">Gestiona y organiza las vulnerabilidades encontradas</p>
								</div>
								<div className="chip chip--regular">
									<span className="chip-text"><strong>Informe ID:</strong> {reportId}</span>
								</div>
							</div>
							<div className="">
								<button className="button">Test</button>
							</div>
						</div>
					</section>
					<section className="board-lists">
						{boardData.map((list, index) => (
							<div key={index} className="board-list card" data-list={list.id}>
								<div className="list-header">
									<h3 className="list-title ptext">{list.title}</h3>
									<div className="list-actions">
										<span className="action-count">{list.tasks.length}</span>
										<button className="action-button">
											<span className="icon icon-more"></span>
										</button>
										<ul className="actions-menu">
											<li className="action-item">Eliminar lista</li>
											<li className="action-item">Archivar lista</li>
										</ul>
									</div>
								</div>
								<ul className="task-list">
									{list.tasks.filter((task) => !task.archived ).map((task, index) => (
										<li key={index} className="task-item" data-task={task.id}>
											<div className="task-header">
												<h4 className="task-title">{task.title}</h4>
												<div className="task-info">
													<span className="chip chip--type">
														<span className="chip-text">{task.type}</span>
													</span>
													<span className="chip chip--warning">
														<span className="chip-text">{task.severity}</span>
													</span>
												</div>
											</div>
										</li>
									))}
								</ul>
							</div>
						))}
					</section>
				</>)))}
			</div>
		</div>
	);
}
