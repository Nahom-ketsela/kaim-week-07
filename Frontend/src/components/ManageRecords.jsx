import React, { useState } from "react";
import {
    createDetection,
    getDetectionById,
    updateDetection,
    deleteDetection,
    createTelegramMessage,
    getTelegramMessageById,
    updateTelegramMessage,
    deleteTelegramMessage,
} from "../api";
import "../index.css";

const ManageRecords = () => {
    const [recordType, setRecordType] = useState("detection");
    const [recordId, setRecordId] = useState("");
    const [recordData, setRecordData] = useState({});
    const [fetchedData, setFetchedData] = useState(null);

    const handleChange = (e) => {
        setRecordData({ ...recordData, [e.target.name]: e.target.value });
    };

    const fetchRecordById = async () => {
        try {
            let response;
            if (recordType === "detection") {
                response = await getDetectionById(recordId);
            } else {
                response = await getTelegramMessageById(recordId);
            }
            setFetchedData(response.data);
        } catch (error) {
            console.error("Error fetching record:", error);
            setFetchedData(null);
        }
    };

    const createRecord = async () => {
        try {
            if (recordType === "detection") {
                await createDetection(recordData);
            } else {
                await createTelegramMessage(recordData);
            }
            alert("Record created successfully!");
        } catch (error) {
            console.error("Error creating record:", error);
        }
    };

    const updateRecord = async () => {
        try {
            if (recordType === "detection") {
                await updateDetection(recordId, recordData);
            } else {
                await updateTelegramMessage(recordId, recordData);
            }
            alert("Record updated successfully!");
        } catch (error) {
            console.error("Error updating record:", error);
        }
    };

    const deleteRecord = async () => {
        try {
            if (recordType === "detection") {
                await deleteDetection(recordId);
            } else {
                await deleteTelegramMessage(recordId);
            }
            alert("Record deleted successfully!");
            setFetchedData(null);
        } catch (error) {
            console.error("Error deleting record:", error);
        }
    };

    return (
        <div className="container">
            <h2 className="heading">Manage Records</h2>

            <select
                className="select-input"
                onChange={(e) => setRecordType(e.target.value)}
            >
                <option value="detection">Detection</option>
                <option value="telegram">Telegram Message</option>
            </select>

            <div className="input-group">
                <input
                    type="text"
                    className="text-input"
                    placeholder="Enter ID"
                    value={recordId}
                    onChange={(e) => setRecordId(e.target.value)}
                />
                <button
                    className="button button-primary"
                    onClick={fetchRecordById}
                >
                    Search by ID
                </button>
            </div>

            {fetchedData && (
                <div className="record-container">
                    <h3 className="record-heading">Fetched Record:</h3>
                    <pre>{JSON.stringify(fetchedData, null, 2)}</pre>
                </div>
            )}

            <div className="input-group">
                <input
                    type="text"
                    name="image_name"
                    className="text-input"
                    placeholder="Image Name (for detection)"
                    onChange={handleChange}
                />
                <input
                    type="text"
                    name="message"
                    className="text-input"
                    placeholder="Message (for telegram)"
                    onChange={handleChange}
                />
            </div>

            <div className="flex-buttons">
                <button
                    className="button button-green"
                    onClick={createRecord}
                >
                    Create
                </button>
                <button
                    className="button button-yellow"
                    onClick={updateRecord}
                >
                    Update
                </button>
                <button
                    className="button button-red"
                    onClick={deleteRecord}
                >
                    Delete
                </button>
            </div>
        </div>
    );
};

export default ManageRecords;
