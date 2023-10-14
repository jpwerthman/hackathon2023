import React from "react";

const SvgComponent = ({ w, h, stroke }) => {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">

  <circle cx="30" cy="50" r="30" fill="#FF6F61" />

  <circle cx="70" cy="50" r="30" fill="#FFCB2D" />


  <circle cx="28" cy="50" r="10" fill="white" />
  <circle cx="28" cy="50" r="5" fill="#000" />


  <circle cx="72" cy="50" r="10" fill="white" />
  <circle cx="72" cy="50" r="5" fill="#000" />


  <path d="M60,50 C60,35 45,13 40,50 C40,65 55,90 60,50" fill="orange" />


  <path d="M30,70 Q50,80 70,70" fill="none" stroke="#000" stroke-width="2" />
</svg>




  );
};

export default SvgComponent;
