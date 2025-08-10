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

    if (options.body && method.toUpperCase() !== 'GET') fetchConfig.body = JSON.stringify(options.body)
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
            console.log(response)
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
        const response = await fetchData(`/analyze?domain=${scanDomain}`)
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
}   

export const getReport = async (reportId) => {
    try {
        const response = await fetchData(`/report/${reportId}`)
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
}   

export const getReportBoard = async (reportId) => {
    try {
        const response = await fetchData(`/report/${reportId}/board`)
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
} 

// TASK API CALLS
export const getTask = async (taskId) => {
    try {
        const response = await fetchData(`/task/${taskId}`)
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
} 

export const removeTask = async (taskId) => {
    try {
        const response = await fetchData(`/task/${taskId}`, {method: 'DELETE'})
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
}  

// LIST API CALLS
export const getList = async (listId) => {
    try {
        const response = await fetchData(`/list/${listId}`)
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
} 

export const removeList = async (taskId) => {
    try {
        const response = await fetchData(`/list/${taskId}`, {method: 'DELETE'})
        return response
    } catch (error) {
        console.error(`Failed to fetch from ${endpoint}:`, error);
        throw error;
    }
}  