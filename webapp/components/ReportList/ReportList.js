import ReportResume from '@components/ReportResume/ReportResume'
import Link from 'next/link'

export default function Reportlist({ reportCount, reportData, onDeleteReport }) {

    return (
        <section className="report-list card">
            <h2 className="card-title">Lista de informes ({reportCount})</h2>
            {reportCount <= 0 ? (
                <div className="empty-reports">
                    <h3 className="empty-title ptext">No se han encontrado informes.</h3>
                    <p className="empty-subtitle stext">Para añadir un nuevo informe, se debe realizar el escaneo de una URL / dominio previamente.</p>
                    <Link href="/" className="button button-secondary">
                        Nuevo escaneo
                    </Link>
                </div>
            ) : reportData.length <= 0 ? (
                <div className="empty-reports">
                    <h3 className="empty-title ptext">No se han encontrado informes con los filtros aplicados.</h3>
                    <p className="empty-subtitle stext">Modifica los filtros para ver más informes.</p>
                </div>
            ) : (
                reportData.map(report => (
                    <ReportResume
                        key={report.id}
                        report={report}
                        onDeleteReport={onDeleteReport}
                    />
                ))
            )}
        </section>
    )
} 