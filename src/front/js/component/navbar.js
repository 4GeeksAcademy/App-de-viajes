import React from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons'

export const Navbar = () => {
	return (
		<nav className="navbar navbar-light ">
			<div className="container">
				<Link to="/" className="link-navbar-brand">
					<span className="navbar-brand mb-0 fs-4 ">TraveLink</span>
				</Link>
				<div className="">
					<Link to="/demo">
						<button className="btn btn-travelink rounded-pill">Check the Context in action</button>
					</Link>
					<FontAwesomeIcon className="ms-4" icon={faMagnifyingGlass} style={{color: "#4dd7fa",}} />
				</div>
			</div>
		</nav>
	);
};
