import Link from 'next/link'

export default function Header() {
	return (
		<nav id="header">
			<Link href="/" className="header-logo">
				<span className="icon icon-webscavul"></span>
			</Link>
			<div className="header-links">
				<Link href="/" className="header-link">
					Escaner
				</Link>
				<Link href="/reports" className="header-link">
					Mis reportes
				</Link>
			</div>
		</nav>
	)
}