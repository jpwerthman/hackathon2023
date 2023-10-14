import React from "react";
import BotResponse from "./BotResponse";

const IntroSection = () => {
  return (
    <div id="introsection">
      <h1>
        Introducing your Financial Manager
        <BotResponse response=" - The Ultimate Financial AI Assistant" />
      </h1>
      <h2>
        A cutting-edge AI-powered app that provides instant answers to any
        question you may have about your transactions. Whether its income or expenses, subscriptions or one time payments, your Financial Manager has the answers.
      </h2>
      Features:
      <ul>
        <li>Instant answers to any Financial question</li>
        <li>User-friendly interface</li>
        <li>Available 24/7</li>
      </ul>
      <p>
        Say goodbye to navigating your complex banking app, and say hello to your Personal Finance Manager,
        your personal AI assistant. Try it now and see for yourself how your Finance Manager
        can make your life easier.
      </p>
    </div>
  );
};

export default IntroSection;
