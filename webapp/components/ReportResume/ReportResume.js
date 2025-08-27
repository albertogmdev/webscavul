import Link from 'next/link'
import { useState, useEffect } from 'react'

export default function ReportResume({ report, onDeleteReport }) {
    const scanTypes = {
        "full": "Completo",
        "headers": "Cabeceras"
    }
    const [isActionMenuOpen, setActionMenuOpen] = useState(false)
    const [certificateInfo, setCertificateInfo] = useState(null)

    useEffect(() => {
        if (report.ssl_info && !report.ssl_info.error) {
            setCertificateInfo({
                chip: "success",
                text: "Válido"
            })
        }
        else {
            setCertificateInfo({
                chip: "error",
                text: "No válido"
            })
        }
    }, [report])

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

    const handleReportDelete = async () => {
        const isDeleted = await onDeleteReport(report.id)
        if (isDeleted) setActionMenuOpen(false)
    }

    return (
        <div className="report-resume">
            <div className="chip chip--regular">
                <span className="chip-text">
                    <strong>Informe ID:</strong> {report.id}
                </span>
            </div>
            <div className="resume-header">
                <div className="header-info">
                    <span className="info-icon icon icon-globe"></span>
                    <div className="info-main">
                        <h3 className="report-title ptext">
                            <a href={report.full_domain} target="_blank" rel="noopener noreferer">
                                {report.full_domain}
                            </a>
                        </h3>
                        <p className="report-protocol stext">{report.protocol}</p>
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
                        <li className="action-item" onClick={handleReportDelete}>Eliminar informe</li>
                    </ul>
                )}
            </div>
            <div className="resume-type">
                <p>Tipo de escaneo: </p>
                <div className="chip chip--info">
                    <span className="chip-text"> {scanTypes[report.type]} </span>
                </div>
            </div>
            <div className="resume-content">
                <div className="resume-item">
                    <h4 className="item-title">Estado</h4>
                    <div className="chip chip--success">
                        <span className="chip-text">
                            Completado
                        </span>
                    </div>
                </div>
                <div className="resume-item">
                    <h4 className="item-title">Certificado</h4>
                    {certificateInfo && (
                        <div className={`chip chip--${certificateInfo.chip}`}>
                            <span className="chip-text">
                                {certificateInfo.text}
                            </span>
                        </div>
                    )}
                </div>
                {report.type === "full" && (
                    <div className="resume-item">
                        <h4 className="item-title">Vulnerabilidades</h4>
                        <p className="item-text">{report.vulnerabilities} encontradas</p>
                    </div>
                )}
                <div className="resume-item">
                    <h4 className="item-title">Fecha</h4>
                    <p className="item-text">{report.created_at.split("T")[0].split("-").reverse().join("/")}</p>
                </div>
            </div>
            <div className="resume-buttons">
                <Link href={`/report/${report.id}`} className="button button-primary">
                    Ver informe
                </Link>
                {report.type === "full" && (
                    <Link href={`/report/${report.id}/board`} className="button button-secondary">
                        Ver tablero
                    </Link>
                )}
            </div>
        </div>
    )
} 