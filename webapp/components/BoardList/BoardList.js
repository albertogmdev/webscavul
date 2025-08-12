import { useEffect, useState } from "react"
import Task from "@components/Task/Task"

export default function BoardList({list, lists, onDeleteList, onDeleteTask, onUpdateList, onTaskMove}) {
    const [isActionMenuOpen, setActionMenuOpen] = useState(false)

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

    return (
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
                        <li className="action-item" onClick={() => console.log("holaaaaa")}>Archivar lista</li>
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
	);
}