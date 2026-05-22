export interface Program {
  id: number;
  name: string;
  description: string;
  is_active: boolean;
  stages_count: number;
  tasks_count: number;
  created_at: string;
}

export interface InstanceSummary {
  id: number;
  employee: number;
  program: number;
  status: string;
  progress_percent: number;
  started_at: string;
  completed_at: string | null;
}

export interface TaskItem {
  id: number;
  title: string;
  task_type: string;
  is_required: boolean;
  due_date: string;
  is_completed: boolean;
}

export interface StageItem {
  id: number;
  name: string;
  order: number;
  tasks: TaskItem[];
}

export interface InstanceDetail {
  id: number;
  employee: {
    id: number;
    full_name: string;
    email: string;
    department: string;
    position: string;
    start_date: string | null;
  };
  program: { id: number; name: string; description: string; is_active: boolean };
  status: string;
  progress_percent: number;
  started_at: string;
  completed_at: string | null;
  stages: StageItem[];
}

export interface Analytics {
  total_instances: number;
  by_status: { in_progress: number; completed: number; overdue: number };
  average_progress: number;
  programs: { id: number; name: string; instance_count: number; active_count: number }[];
  employees_in_onboarding: number;
}

export interface UserMe {
  id: number;
  username: string;
  email: string;
  full_name: string;
  role: string;
}
