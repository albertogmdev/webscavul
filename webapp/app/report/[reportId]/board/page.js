"use client"

import { useParams } from 'next/navigation'
import { useEffect, useState } from "react"
import { getReportBoard, deleteList, createList, moveTask, deleteTask } from '@/api'
import BoardList from '@components/BoardList/BoardList'
import Modal from "@components/Modal/Modal"

export default function ReportBoard() {
	const params = useParams()
	const reportId = params.reportId

	const [boardData, setBoardData] = useState(null)
	const [listInfo, setListInfo] = useState(null)
	const [openCreateList, setCreateListOpen] = useState(false)
	const [error, setError] = useState(null)
	const [loading, setLoading] = useState(null)
	const [newListName, setNewListName] = useState("")

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


	useEffect(() => {
		if (!boardData) return

		boardListInfo(boardData)
	}, [boardData])

	const handleDeleteList = async (listId) => {
		try {
			const response = await deleteList(listId)

			if (response.status == 200) {
				setBoardData(boardData.filter((list) => list.id != listId))
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
				setBoardData(prevBoardData => {
					return prevBoardData.map((list, index) => {
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
				})

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

	const handleUpdateList = (listId) => {
		console.log(listId)
	}

	const handleMoveTask = async (taskId, listOrigin, listDestination) => {
		try {
			const response = await moveTask(taskId, listDestination)

			if (response.status == 200) {
				let movedTask = null
				setBoardData(prevBoardData => {
					const newBoardData = prevBoardData.map(list => {
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
						return newBoardData.map(list => {
							// Add task in new list
							if (list.id === listDestination) {
								return { ...list, tasks: [...list.tasks, movedTask] }
							}
							return list
						})
					}

					return newBoardData
				})
				
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

				setBoardData(prevBoardData => [...prevBoardData, newList])
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
