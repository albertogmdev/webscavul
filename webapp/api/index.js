const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export async function fetchData(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    }

    const fetchConfig = {
        method: options.method || 'GET',
        ...options,
        headers, 
    }

    if (options.body && options.method.toUpperCase() !== 'GET') fetchConfig.body = JSON.stringify(options.body)
    else if (options.body && method.toUpperCase() === 'GET') {
        console.log("ERROR: GET request receive a option body object. Query params should be used instead")
        delete fetchConfig.body
    }
    
    try {
        let responseData = {}
        const response = await fetch(`${BASE_URL}${endpoint}`, fetchConfig)
        
        if (response.ok) {
            const jsonData = await response.json()
            responseData = {
                status: response.status,
                message: jsonData.message,
                data: jsonData.data
            }
        }
        else {
            const errorData = await response.json().catch(() => ({ message: 'An unknown API error occurred.' }));
            responseData = {
                status: response.status,
                error: errorData.detail.message
            }
        }

        return responseData
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
}

// REPORT API CALLS
export const createReport = async (scanDomain) => {
    try {
        const endpoint = `/analyze?domain=${scanDomain}`
        const response = await fetchData(endpoint)
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
}  

export const deleteReport = async (reportId) => {
    try {
        const endpoint = `/report/${reportId}`
        const response = await fetchData(endpoint, {method: 'DELETE'})
        return response
    } catch (error) { 
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
}

export const getAllReports = async () => {
    try {
        const endpoint = `/reports`
        const response = await fetchData(endpoint)
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
}   

export const getReport = async (reportId) => {
    try {
        const endpoint = `/report/${reportId}`
        const response = await fetchData(endpoint)
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
}   

export const getReportBoard = async (reportId) => {
    try {
        const endpoint = `/report/${reportId}/board`
        const response = await fetchData(endpoint)
        return response
    } catch (error) {
        console.error(`Failed to fetch data`, error);
        throw error;
    }
} 

// TASK API CALLS
export const getTask = async (taskId) => {
    try {
        const endpoint = `/task/${taskId}`
        const response = await fetchData(endpoint)
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
} 

export const deleteTask = async (taskId) => {
    try {
        const endpoint = `/task/${taskId}`
        const response = await fetchData(endpoint, {method: 'DELETE'})
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
}  

export const moveTask = async (taskId, listId) => {
    try {
        const endpoint = `/task/${taskId}`
        const body = { "list_id": listId }
        const response = await fetchData(endpoint, {method: 'PUT', body: body})
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error)
        throw error
    }
}  

// LIST API CALLS
export const getList = async (listId) => {
    try {
        const endpoint = `/list/${listId}`
        const response = await fetchData(endpoint)
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
} 

export const deleteList = async (taskId) => {
    try {
        const endpoint = `/list/${taskId}`
        const response = await fetchData(endpoint, {method: 'DELETE'})
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
}  

export const updateList = async (listId, listName) => {
    try {
        const endpoint = `/list/${listId}`
        const body = { "title": listName }
        const response = await fetchData(endpoint, {method: 'PUT', body: body})
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
}  

export const createList = async (listName, reportId) => {
    try {
        const body = {
            "title": listName,
            "report_id": reportId
        }
        const endpoint = `/list/`
        const response = await fetchData(endpoint, {method: 'POST', body: body})
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
} 