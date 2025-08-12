

export default function BoardFilter({onFilter}) {
    

    return (
        <div className="card board-filter">
            <div className="filter-content">
                <div className="filter-item">
                    <p className="item-label">Tipo</p>
                    <input 
                        className="filter-name"
                        type="text" 
                        placeholder="Buscar por nombre..." 
                        onChange={(e) => onFilter('name', e.target.value)} 
                    />
                </div>
                <div className="filter-item">
                    <p className="item-label">Importancia</p>
                    <select 
                        className="filter-severity"
                        onChange={(e) => onFilter('severity', e.target.value)}
                    >
                        <option value="">Todas</option>
                        <option value="information">Informativo</option>
                        <option value="low">Bajo</option>
                        <option value="medium">Media</option>
                        <option value="high">Alta</option>
                    </select>
                </div>
            </div>
        </div>
    )
}