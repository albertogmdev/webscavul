import { useEffect } from "react"

export default function Modal({ title, modalClass = "", children, onModalClose }) {

    const handleBackdropClick = (event) => {
        if (event.target === event.currentTarget) onModalClose()
    }

    useEffect(() => {
        document.body.classList.add("modal-open")
        return () => { document.body.classList.remove("modal-open") }
    }, [])
    
    return (
        <div className={`modal ${modalClass}`} onClick={handleBackdropClick}>
            <div className="modal-content">
                <button className="modal-close" onClick={onModalClose}>
                    <span className="icon icon-close"></span>
                </button>
                <div className="modal-title">{title}</div>
                <div className="modal-body">
                    {children}
                </div>
            </div>
        </div>
    )
}