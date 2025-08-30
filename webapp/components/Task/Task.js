import { useEffect, useState, useRef } from "react"
import { askModel } from "@utils/groq"
import Code from "@components/Code/Code"
import Modal from "@components/Modal/Modal"
import TaskTag from "@components/TaskTag/TaskTag"
import ReactMarkdown from 'react-markdown'

export default function Task({ task, listId, lists, onDeleteTask, onTaskMove }) {
    const [isTaskOpen, setTaskOpen] = useState(false)
    const [isActionMenuOpen, setActionMenuOpen] = useState(false)
    const [taskSolution, seTaskSolution] = useState("")
    const [taskContext, seTaskContext] = useState("")

    useEffect(() => {
        const handleOutsideClick = (event) => {
            const target = event.target
            if (!isActionMenuOpen) return
            if (target.classList.contains("action-button") || target.closest(".action-button")) return

            if (!target.classList.contains("action-item")
                && !target.closest(".actions-menu")) {
                setActionMenuOpen(false)
            }
        }

        document.addEventListener('mousedown', handleOutsideClick)
        return () => { document.removeEventListener('mousedown', handleOutsideClick) }
    }, [isActionMenuOpen])

    const handleAskModel = async (type) => {
        try {
            if (type === "solution" && taskSolution) return
            if (type === "context" && taskContext) return

            const query = `Vulnerabiliad: ${task.title}, Importancia: ${task.severity}, Información proporcionada: ${task.details}, Código asociado: ${task.code || "No hay código asociado."}`
            const modelAnswer = await askModel(query, type)

            if (type === "solution") seTaskSolution(modelAnswer)
            else if (type === "context") seTaskContext(modelAnswer)
        } catch (error) {
            console.error("Error fetching from AI:", error)
        }
    }

    const handleTaskDelete = async () => {
        const isDeleted = await onDeleteTask(task.id, listId)
        if (isDeleted) setTaskOpen(false)
    }

    const handleTaskMove = async (listDestination) => {
        const isMoved = await onTaskMove(task.id, listId, listDestination)
        if (isMoved) setTaskOpen(false)
    }

    const handleAddComment = (event) => {
        event.preventDefault()
        const comment = event.target.comment.value.trim()
        if (!comment) return
    }

    return (
        <>
            <li
                className="task-item" data-task={task.id}
                onClick={() => setTaskOpen(true)}
            >
                <div className="task-header">
                    <h4 className="task-title">{task.title}</h4>
                    <div className="task-info">
                        <TaskTag type={task.type} />
                        <TaskTag severity={task.severity} />
                    </div>
                </div>
            </li>
            {isTaskOpen && (
                <Modal
                    title={task.title}
                    modalClass="modal-task"
                    onModalClose={() => setTaskOpen(false)}
                >
                    <div className="task-tags">
                        <div className="tags-info">
                            <div className="tag-row">
                                <p>Tipo:</p>
                                <TaskTag type={task.type} />
                            </div>
                            <div className="tag-row">
                                <p>Importancia: {isActionMenuOpen}</p>
                                <TaskTag severity={task.severity} />
                            </div>
                        </div>
                        <button
                            className="action-button"
                            onClick={() => setActionMenuOpen(!isActionMenuOpen)}
                        >
                            <span className="icon icon-more"></span>
                        </button>
                        {isActionMenuOpen && (
                            <ul className="actions-menu">
                                <li className="action-item" onClick={handleTaskDelete}>Eliminar tarea</li>
                                {lists.filter((listInfo => listInfo.id != listId)).map((listInfo, index) => (
                                    <li
                                        key={index}
                                        className="action-item"
                                        onClick={() => handleTaskMove(listInfo.id)}
                                    >
                                        Movar tarea a {listInfo.title}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                    <div className="task-content scroll-section">
                        <div className="task-details">
                            <p className="content-title">Detalles</p>
                            <div className="content-info">
                                {task.details || "No se han especificado detalles."}
                            </div>
                        </div>
                        {task.location && (
                            <div className="task-location">
                                <p className="content-title">Ubicación</p>
                                <div className="content-info">{task.location}</div>
                            </div>
                        )}
                        {task.code && (
                            <div className="task-code">
                                <p className="content-title">Código</p>
                                <div className="content-info">
                                    <Code html={task.code} />
                                </div>
                            </div>
                        )}
                        <div className="task-generation task-context">
                            <p className="content-title">¿Qué es esto?</p>
                            {taskContext ? (
                                <ReactMarkdown className="generated-content">{taskContext}</ReactMarkdown>
                            ) : (
                                <button
                                    className="generate-button"
                                    onClick={() => handleAskModel("context")}
                                >
                                    Generar explicación
                                </button>
                            )}
                        </div>
                        <div className="task-generation task-solution">
                            <p className="content-title">¿Cómo solucionarlo?</p>
                            {taskSolution ? (
                                <ReactMarkdown className="generated-content">{taskSolution}</ReactMarkdown>
                            ) : (
                                <button
                                    className="generate-button"
                                    onClick={() => handleAskModel("solution")}
                                >
                                    Generar solución
                                </button>
                            )}
                        </div>
                        {/* <div className="task-comments">
                            <p className="content-title">Comentario</p>
                            <div className="content-info">{task.comments || "No se ha añadido ningún comentario."}</div>
                            <form
                                className="comment-form"
                                onSubmit={handleAddComment}
                            >
                                <textarea
                                    name="comment"
                                    placeholder="Añadir un comentario..."
                                    value={taskComment}
                                    onChange={(e) => setTaskComment(e.target.value)}
                                ></textarea>
                                <button type="submit" className="button button-primary">Añadir</button>
                            </form>
                        </div> */}
                    </div>
                </Modal >
            )
            }
        </>
    )
}