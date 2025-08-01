export interface AssistantResponse {
    success: boolean;
    data?: {
      question: string;
      answer: string;
      projects?: Project[];
      formatted: boolean;
      timestamp: number;
    };
    error?: {
      message: string;
      code: string;
    };
  }
  
  interface Project {
    id: string;
    name: string;
    status: string;
    start_date: string;
    deadline: string;
    progress: number;
  }