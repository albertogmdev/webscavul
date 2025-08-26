import ScannerCard from '@/components/ScannerCard/ScannerCard'

export default function Home() {
	return (
		<div className="page page-home">
			<section className="scan-hero">
				<div className="container">
					<div className="hero-content">
						<h1 className="home-title ptext">WEBSCAVUL</h1>
						<p className="home-description stext">Encuentra y gestiona fallos y vulnerabilidades en tu página web, solo con introducir la URL.</p>
					</div>
					<ScannerCard />
				</div>
			</section>
			<section className="home-info">
				<div className="container">
					
				</div>
			</section>
		</div>
	)
}
