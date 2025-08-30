"use client"

import { useParams } from 'next/navigation'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from "react"
import { getReportBoard, deleteList, createList, moveTask, deleteTask, updateList } from '@/api'
import Link from 'next/link'
import BoardList from '@components/BoardList/BoardList'
import BoardFilter from '@components/BoardFilter/BoardFilter'
import Modal from "@components/Modal/Modal"

export default function ReportBoard() {
	const params = useParams()
	const router = useRouter()
	const reportId = params.reportId

	const [boardData, setBoardData] = useState(null)
	const [filteredBoardData, setFilteredBoardData] = useState(null)
	const [filterName, setFilterName] = useState("")
	const [filterSeverity, setFilterSeverity] = useState("")
	const [listInfo, setListInfo] = useState(null)
	const [openCreateList, setCreateListOpen] = useState(false)
	const [error, setError] = useState(null)
	const [loading, setLoading] = useState(null)
	const [newListName, setNewListName] = useState("")

	useEffect(() => {
		const getBoardInfo = async () => {
			try {
				const response = await getReportBoard(reportId)
				if (response.status == 200) {
					// Redirect to report page when scan type is not "full"
					if (response.data.board && response.data.board === "noboard") {
						router.push(`/report/${reportId}`)
						return
					}

					const board = response.data.board

					setBoardData(board)
					setFilteredBoardData(board)
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

		getBoardInfo()
		document.title = "Tablero | WebScavul"
	}, [reportId])


	useEffect(() => {
		if (!boardData) return

		boardListInfo(boardData)
	}, [boardData])

	const handleDeleteList = async (listId) => {
		try {
			const response = await deleteList(listId)

			if (response.status == 200) {
				const afterDelete = boardData.filter((list) => list.id != listId)

				setBoardData(afterDelete)
				setFilteredBoardData(afterDelete)
				// When modifying the board data, we also need to apply the current filters
				applyFilters(filterName, filterSeverity, afterDelete)
			}
			else {
				console.error("Error deleting list:", err)
			}
		}
		catch (err) {
			console.error("Error deleting list:", err)
		}
	}

	const handleDeleteTask = async (taskId, listId) => {
		try {
			const response = await deleteTask(taskId)

			if (response.status == 200) {
				const afterDelete = boardData.map((list, index) => {
					if (list.id === listId) {
						const tasksInOrigin = list.tasks
						const taskIndex = tasksInOrigin.findIndex(task => task.id === taskId)

						if (taskIndex > -1) {
							return {
								...list,
								tasks: [
									...tasksInOrigin.slice(0, taskIndex),
									...tasksInOrigin.slice(taskIndex + 1)
								]
							}
						}
					}
					return list
				})

				setBoardData(afterDelete)
				setFilteredBoardData(afterDelete)
				// When modifying the board data, we also need to apply the current filters
				applyFilters(filterName, filterSeverity, afterDelete)

				return true
			}
			else {
				console.error("Error moving task to list")
				return false
			}
		}
		catch (err) {
			console.error("Error moving task:", err)
			return false
		}
	}

	const handleUpdateList = async (listId, newListName) => {
		if (newListName === "") return

		try {
			const response = await updateList(listId, newListName)

			if (response.status == 200) {
				const afterUpdate = boardData.map((list) => {
					if (list.id === listId) {
						return {
							...list,
							title: newListName
						}
					}
					return list
				})

				setBoardData(afterUpdate)
				setFilteredBoardData(afterUpdate)
				// When modifying the board data, we also need to apply the current filters
				applyFilters(filterName, filterSeverity, afterUpdate)

				return true
			}
			else {
				console.error("Error updating list")
				return false
			}
		}
		catch (err) {
			console.error("Error updating list:", err)
			return false
		}
	}

	const handleMoveTask = async (taskId, listOrigin, listDestination) => {
		try {
			const response = await moveTask(taskId, listDestination)

			if (response.status == 200) {
				let movedTask = null
				let movedData = boardData.map(list => {
					if (list.id === listOrigin) {
						const tasksInOrigin = list.tasks
						const taskIndex = tasksInOrigin.findIndex(task => task.id === taskId)

						// Task is found, save the task with the destination list id
						if (taskIndex > -1) {
							movedTask = { ...tasksInOrigin[taskIndex], list_id: listDestination }
							return {
								...list,
								tasks: [
									...tasksInOrigin.slice(0, taskIndex),
									...tasksInOrigin.slice(taskIndex + 1)
								]
							}
						}
					}
					return list
				})

				if (movedTask) {
					movedData = movedData.map(list => {
						// Add task in new list
						if (list.id === listDestination) {
							return { ...list, tasks: [...list.tasks, movedTask] }
						}
						return list
					})
				}

				setBoardData(movedData)
				setFilteredBoardData(movedData)
				// When modifying the board data, we also need to apply the current filters
				applyFilters(filterName, filterSeverity, movedData)

				return true
			}
			else {
				console.error("Error moving task to list")
				return false
			}
		}
		catch (err) {
			console.error("Error moving task:", err)
			return false
		}
	}

	const handleCreateList = async (event) => {
		event.preventDefault()
		if (newListName === "") return

		try {
			const response = await createList(newListName, reportId)

			if (response.status == 200) {
				const newListId = response.data.list_id
				const newList = {
					"id": newListId,
					"report_id": reportId,
					"title": newListName,
					"tasks": []
				}
				const afterCreate = [...boardData, newList]

				setBoardData(afterCreate)
				setFilteredBoardData(afterCreate)
				// When modifying the board data, we also need to apply the current filters
				applyFilters(filterName, filterSeverity, afterCreate)
				setCreateListOpen(false)
			}
			else {
				console.error("Error deleting list:", err)
			}
		}
		catch (err) {
			console.error("Error deleting list:", err)
		}
	}

	const boardListInfo = (board) => {
		const listInfo = []

		board.map((list) => {
			listInfo.push({
				id: list.id,
				title: list.title
			})
		})

		setListInfo(listInfo)
	}

	const applyFilters = (nameData, severityData, data) => {
		let newBoardData = [...data]

		if (nameData !== "") {
			newBoardData = newBoardData.map(list => {
				return {
					...list,
					tasks: list.tasks.filter(task => task.title.toLowerCase().includes(nameData))
				}
			})
		}

		if (severityData !== "") {
			newBoardData = newBoardData.map(list => {
				return {
					...list,
					tasks: list.tasks.filter(task => task.severity.toLowerCase() === severityData)
				}
			})
		}

		setFilteredBoardData(newBoardData)
	}

	const handleFilter = (type, value) => {
		if (type === "name") setFilterName(value.toLowerCase())
		if (type === "severity") setFilterSeverity(value.toLowerCase())

		const nameData = type === "name" ? value.toLowerCase() : filterName.toLowerCase()
		const severityData = type === "severity" ? value.toLowerCase() : filterSeverity.toLowerCase()
		applyFilters(nameData, severityData, boardData)
	}

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
							<div className="card-content">
								<div className="content-info">
									<div className="info-item info-tasks">
										<span className="info-text">Tareas totales: </span>
										<span className="info-count">
											{boardData.reduce((acc, list) => acc + list.tasks.length, 0)}
										</span>
									</div>
									<div className="info-item info-critical">
										<span className="info-text">Tareas críticas: </span>
										<span className="info-count">
											{boardData.reduce((acc, list) => acc + list.tasks.filter(task => task.severity && task.severity.toLowerCase() === "high").length, 0)}
										</span>
									</div>
								</div>
								<div className="content-buttons">
									<Link
										href={`/report/${reportId}`}
										className="button button-primary"
									>
										Ver informe
									</Link>
									<Link
										href="/reports"
										className="button button-secondary"
									>
										Mis informes
									</Link>
								</div>
							</div>
						</div>
						<BoardFilter
							onFilter={handleFilter}
						/>
					</section>
					<section className="board-lists scroll-section">
						{filteredBoardData.map((list, index) => (
							<BoardList
								key={index}
								list={list}
								lists={listInfo}
								onDeleteList={handleDeleteList}
								onDeleteTask={handleDeleteTask}
								onUpdateList={handleUpdateList}
								onTaskMove={handleMoveTask}
							/>
						))}
						<div className="board-list board-addlist" onClick={() => setCreateListOpen(true)}>
							<div className="addlist-text">Añadir lista</div>
						</div>
					</section>
				</>)))}
			</div>
			{openCreateList && (
				<Modal
					title="Crear una lista"
					modalClass="modal-addlist"
					onModalClose={() => setCreateListOpen(false)}
				>
					<form className="form-addlist" onSubmit={handleCreateList}>
						<input
							className="addlist-name"
							type="text"
							onChange={(event) => { setNewListName(event.target.value) }}
							placeholder="Nombre de la lista"
						/>
						<button className="button button-primary">Añadir</button>
					</form>
				</Modal>
			)}
		</div>
	)
}
