import api from './api';

// This should change depending on the API, not a single interface, TODO
interface Resource {
  id?: string;
  name: string;
  description: string;
}

const apiService = {
  async getData() {
    const response = await api.get('/data');
    return response.data;
  },

  async createResource(payload: Resource) {
    const response = await api.post('/resource', payload);
    return response.data;
  },

  async updateResource(id: string, payload: Partial<Resource>) {
    const response = await api.put(`/resource/${id}`, payload);
    return response.data;
  },

  async deleteResource(id: string) {
    await api.delete(`/resource/${id}`);
  }

  
};

export default apiService;