export default function BoardFilter({onFilter}) {
    return (
        <div className="card section-filter">
            <div className="filter-content">
                <div className="filter-item">
                    <p className="item-label">Nombre</p>
                    <input 
                        className="filter-name"
                        type="text" 
                        placeholder="Buscar por nombre..." 
                        onChange={(e) => onFilter('name', e.target.value)} 
                    />
                </div>
                <div className="filter-item">
                    <p className="item-label">Tipo escaneo</p>
                    <select 
                        className="filter-type"
                        onChange={(e) => onFilter('type', e.target.value)}
                    >
                        <option value="">Todos</option>
                        <option value="full">Completo</option>
                        <option value="headers">Cabeceras</option>
                    </select>
                </div>
                <div className="filter-item">
                    <p className="item-label">Ordenar</p>
                    <select 
                        className="filter-order"
                        onChange={(e) => onFilter('order', e.target.value)}
                    >
                        <option value="">Sin orden</option>
                        <option value="date_asc">Fecha asc.</option>
                        <option value="date_desc">Fecha desc.</option>
                    </select>
                </div>
            </div>
        </div>
    )
}