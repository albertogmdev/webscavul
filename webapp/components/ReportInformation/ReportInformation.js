export default function ReportInformation({ reportData, sslData }) {
    return (
        <section className="report-information">
            <div className="card">
                <h2 className="card-title">Información general y certificado SSL</h2>
                <div className="information-content">
                    <div className="content-col general-info">
                        <ul className="info-table">
                            <h3 className="table-header">Información general</h3>
                            <li className="table-item">
                                <h4 className="label stext">Dominio</h4>
                                <p className="value ptext">{reportData.domain}</p>
                            </li>
                            <li className="table-item">
                                <h4 className="label stext">URL</h4>
                                <p className="value ptext">{reportData.full_domain}</p>
                            </li>
                            <li className="table-item">
                                <h4 className="label stext">Dirección IP</h4>
                                <p className="value ptext">{reportData.ip}</p>
                            </li>
                            <li className="table-item">
                                <h4 className="label stext">Protocolo</h4>
                                <p className="value ptext">{reportData.protocol}</p>
                            </li>
                        </ul>
                    </div>
                    <div className="content-col ssl-info">
                        {sslData ? (
                            <ul className="info-table">
                                <h3 className="table-header">SSL y TLS</h3>
                                {sslData && Object.entries(sslData).map(([key, value]) => (
                                    <li key={key} className="table-item">
                                        <h4 className="label stext">{key}</h4>
                                        <p className="value ptext">{value}</p>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <div className="ssl-error">
                                <p className="error-text">No se pudo obtener información del certificado SSL.</p>
                                <p className="error-details">Asegúrate de que el sitio web tenga un certificado SSL válido.</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </section>
    )
}