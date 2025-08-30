"use client"

import Link from 'next/link'
import { useRef } from "react"

export default function Header() {
	const darkIcon = useRef(null)
	const lightIcon = useRef(null)

	const handleThemeToggle = () => {
		const htmlElement = document.getElementsByTagName('html')[0]
		htmlElement.classList.toggle('theme-light')
		darkIcon.current.classList.toggle('hidden')
		lightIcon.current.classList.toggle('hidden')
	}
		
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
					Mis informes
				</Link>
				<button 
					id="theme-button"
					className="theme-button"
					title="Cambiar tema"
					onClick={handleThemeToggle}
				>
					<span className="icon icon-light" ref={darkIcon}></span>
					<span className="icon icon-dark hidden" ref={lightIcon}></span>
				</button>
			</div>
		</nav>
	)
}