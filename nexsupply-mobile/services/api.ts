const API_BASE = "https://app.nexsupply.net";

export interface AnalyzeRequest {
  product_name?: string;
  query?: string;
  image_url?: string;
  mode?: string;
  [key: string]: any;
}

export interface AnalyzeResponse {
  success: boolean;
  data?: any;
  error?: string;
}

export async function analyze(body: AnalyzeRequest): Promise<AnalyzeResponse> {
  try {
    const res = await fetch(API_BASE + "/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      throw new Error(`analyze failed: ${res.status} ${res.statusText}`);
    }

    return await res.json();
  } catch (error) {
    console.error("API Error:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}

export async function requestConsultation(body: {
  email: string;
  name?: string;
  product?: string;
  message?: string;
}): Promise<AnalyzeResponse> {
  try {
    const res = await fetch(API_BASE + "/api/consultation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      throw new Error(`consultation request failed: ${res.status} ${res.statusText}`);
    }

    return await res.json();
  } catch (error) {
    console.error("API Error:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}



