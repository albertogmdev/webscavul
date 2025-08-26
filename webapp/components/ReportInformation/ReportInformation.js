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
                                <a
                                    className="value ptext"
                                    href={reportData.domain.split("/")[0]}
                                    target="_blank" rel="noopener noreferer"
                                >
                                    {reportData.domain.split("/")[0]}
                                </a>

                            </li>
                            <li className="table-item">
                                <h4 className="label stext">URL</h4>
                                <a
                                    className="value ptext"
                                    href={reportData.full_domain}
                                    target="_blank" rel="noopener noreferer"
                                >
                                    {reportData.full_domain}
                                </a>
                            </li>
                            <li className="table-item">
                                <h4 className="label stext">Dirección IP</h4>
                                <div className="valueip">
                                    {reportData.ip ? (
                                        reportData.ip.map((ip, index) => (
                                            <a
                                                key={index}
                                                className="value ptext"
                                                href={`//${ip}`}
                                                target="_blank" rel="noopener noreferer"
                                            >
                                                {ip}
                                            </a>
                                        ))) : (
                                        <span>No disponible</span>
                                    )}
                                </div>
                            </li>
                            {reportData.alias && (
                                <li className="table-item">
                                    <h4 className="label stext">Alias</h4>
                                    <div className="valuealias">
                                        {reportData.alias.map((alias, index) => (
                                            <a
                                                key={index}
                                                className="value ptext"
                                                href={`//${alias}`}
                                                target="_blank" rel="noopener noreferer"
                                            >
                                                {alias}
                                            </a>
                                        ))}
                                    </div>
                                </li>
                            )}
                            <li className="table-item">
                                <h4 className="label stext">Protocolo</h4>
                                <p className="value ptext">{reportData.protocol}</p>
                            </li>
                            {reportData.server && (
                                <li className="table-item">
                                    <h4 className="label stext">Servidor</h4>
                                    <p className="value ptext">{reportData.server}</p>
                                </li>
                            )}
                            {reportData.generator && (
                                <li className="table-item">
                                    <h4 className="label stext">Generador</h4>
                                    <p className="value ptext">{reportData.generator}</p>
                                </li>
                            )}
                            {reportData.powered && (
                                <li className="table-item">
                                    <h4 className="label stext">Tecnología</h4>
                                    <p className="value ptext">{reportData.powered}</p>
                                </li>
                            )}
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