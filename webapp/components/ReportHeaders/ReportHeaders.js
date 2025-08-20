export default function ReportHeaders({ headerData }) {
    return (
        <section className="report-headers">
            <div className="card">
                <h2 className="card-title">Análisis de cabeceras HTTP</h2>
                <ul className="headers-list">
                    {headerData && headerData.headers && headerData.headers.length > 0 && (
                        headerData.headers.map((header, index) => (
                            <li key={index} className="header-item">
                                <div className="item-content">
                                    <h3 className="item-title">{header.name}</h3>
                                    <p className="item-description stext">{header.description}</p>
                                    {header.value && (<div className="item-value">{[].concat(header.value).join("; ")}</div>)}
                                </div>
                                <div className="item-chip">
                                    {header.correct && header.enabled
                                        || header.name === "Refresh" && !header.enabled ? (
                                        <div className="chip chip--success">
                                            <span className="chip-text">Correcto</span>
                                        </div>
                                    ) : (header.severity === "warning" ? (
                                        <div className="chip chip--warning">
                                            <span className="chip-text">Warning</span>
                                        </div>
                                    ) : (header.severity === "recommendation" || header.severity === "info" ? (
                                        <div className="chip chip--info">
                                            <span className="chip-text">Recomendado</span>
                                        </div>
                                    ) : (
                                        <div className="chip chip--error">
                                            <span className="chip-text">Crítico</span>
                                        </div>
                                    )))}
                                </div>
                            </li>
                        ))
                    )}
                </ul>
            </div>
        </section>
    )
}