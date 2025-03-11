import React, { useEffect, useState } from "react";
import { getDetections } from "../api";

const DetectionsTable = () => {
    const [detections, setDetections] = useState([]);

    useEffect(() => {
        getDetections().then(setDetections);
    }, []);

    return (
        <div>
            <h2>Detections</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th><th>Image Name</th><th>Class ID</th><th>Confidence</th>
                    </tr>
                </thead>
                <tbody>
                    {detections.map((detection) => (
                        <tr key={detection.id}>
                            <td>{detection.id}</td>
                            <td>{detection.image_name}</td>
                            <td>{detection.class_id}</td>
                            <td>{detection.confidence}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default DetectionsTable;
