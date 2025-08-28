export default function Footer() {
    return (
        <footer className="footer">
            <div className="container">
                <div className="footer-content">
                    <p className="footer-title">Webscavul</p>
                    <div className="footer-text">
                        Aplicación desarrollada por&nbsp;
                        <a 
                            href="https://github.com/albertogmdev" 
                            className="author-link" 
                            target="_blank" 
                            rel="noopener noreferrer">
                            albertogmdev
                        </a>.
                    </div>
                    <div className="footer-links">
                        <a href="https://github.com/albertogmdev" className="footer-link" target="_blank" rel="noopener noreferrer">
                            <span className="icon icon-github footer-icon" title="GitHub"></span>
                        </a>
                        <a href="https://www.linkedin.com/in/albertogonzalezmartinez" className="footer-link" target="_blank" rel="noopener noreferrer">
                            <span className="icon icon-linkedin footer-icon" title="Linkedin"></span>
                        </a>
                    </div>
                </div>
            </div>
        </footer>
    );
}