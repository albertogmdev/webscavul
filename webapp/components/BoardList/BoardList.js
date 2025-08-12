import { useEffect, useState } from "react"
import Task from "@components/Task/Task"
import Modal from "@components/Modal/Modal"

export default function BoardList({list, lists, onDeleteList, onDeleteTask, onUpdateList, onTaskMove}) {
    const [isActionMenuOpen, setActionMenuOpen] = useState(false)
    const [openUpdateList, setOpenUpdateList] = useState(false)
    const [newListName, setNewListName] = useState("")

    useEffect(() => {
		const handleOutsideClick = (event) => {
            const target = event.target
			if (!isActionMenuOpen) return
            if (target.classList.contains("action-button") || target.closest(".action-button")) return

			if (!target.classList.contains("action-item")
				&& !target.closest(".actions-menu")){
				setActionMenuOpen(false)
			}
		}

		document.addEventListener('mousedown', handleOutsideClick)
		return () => { document.removeEventListener('mousedown', handleOutsideClick) }
	}, [isActionMenuOpen])

    const handleListDelete = () => {
        onDeleteList(list.id)
    }

    const handleListUpdate = async (event) => {
        event.preventDefault()
        if (newListName.trim() === "" || newListName === list.title) {
            console.warn("New list name is empty or unchanged.")
            return
        }

        const isUpdated = await onUpdateList(list.id, newListName)
        if (isUpdated) {
            setOpenUpdateList(false)
            setNewListName("")
        }
    }

    return (
        <>
		<div className="board-list card" data-list={list.id}>
            <div className="list-header">
                <h3 className="list-title ptext">{list.title}</h3>
                <div className="list-actions">
                    <span className="action-count">{list.tasks.length}</span>
                    <button 
                        className="action-button"
                        onClick={() => setActionMenuOpen(!isActionMenuOpen)}
                    >
                        <span className="icon icon-more"></span>
                    </button>
                    { isActionMenuOpen && (
                    <ul className="actions-menu">
                        <li className="action-item" onClick={handleListDelete}>Eliminar lista</li>
                        <li className="action-item" onClick={() => setOpenUpdateList(true)}>Editar lista</li>
                    </ul>
                    )}
                </div>
            </div>
            <ul className="task-list">
                {list.tasks.filter((task) => !task.archived ).map((task, index) => (
                    <Task
                        key={index}
                        task={task}
                        listId={list.id}
                        lists={lists}
                        onDeleteTask={onDeleteTask}
                        onTaskMove={onTaskMove}
                    />
                ))}
            </ul>
        </div>
        {openUpdateList && (
            <Modal
                title={`Editar la lista ${list.title}`}
                modalClass="modal-updatelist"
                onModalClose={() => setOpenUpdateList(false)}
            >
                <form className="form-addlist" onSubmit={handleListUpdate}>
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
        </>
	)
}