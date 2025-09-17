import React, {SyntheticEvent} from "react";
import "./Card.css";
import SubmitData from "../SubmitData/SubmitData";
import type { jsx } from "react/jsx-runtime";

interface Props{
    title : string;
    onCollectionCreate: (e: SyntheticEvent) => void;
}

const Card: React.FC<Props> = ({
    title,
    onCollectionCreate,
}:Props):jsx.Element => {
    return (
        <div>
            <p>"Hello"</p>
        </div>
    )
}