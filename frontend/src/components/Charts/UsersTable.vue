<template>
  <div class="users-table">
    <div class="table-header">
      <h4>{{ title }}</h4>
      <div class="table-actions">
        <button class="btn btn-sm" @click="exportUsers">
          <i class="fas fa-download"></i>
          Экспорт
        </button>
        <button class="btn btn-sm btn-primary" @click="$emit('add-user')">
          <i class="fas fa-plus"></i>
          Добавить
        </button>
      </div>
    </div>
    
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th 
              v-for="column in columns" 
              :key="column.key"
              :class="['column-header', column.sortable ? 'sortable' : '']"
              @click="column.sortable ? sortTable(column.key) : null"
            >
              <div class="header-content">
                {{ column.title }}
                <span 
                  v-if="column.sortable" 
                  class="sort-icon"
                  :class="getSortIcon(column.key)"
                >
                  <i class="fas fa-sort"></i>
                </span>
              </div>
            </th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in paginatedUsers" :key="user.id">
            <td>
              <div class="user-cell">
                <div class="user-avatar">
                  <img 
                    :src="user.avatar || '/default-avatar.png'" 
                    :alt="user.name"
                    @error="handleImageError"
                  >
                </div>
                <div class="user-info">
                  <div class="user-name">{{ user.name }}</div>
                  <div class="user-email">{{ user.email }}</div>
                </div>
              </div>
            </td>
            <td>
              <span class="status-badge" :class="`status-${user.status}`">
                {{ getUserStatus(user.status) }}
              </span>
            </td>
            <td>{{ formatDate(user.joinDate) }}</td>
            <td>
              <div class="progress-cell">
                <div class="progress-bar">
                  <div 
                    class="progress-fill" 
                    :style="{ width: user.activity + '%' }"
                  ></div>
                </div>
                <span class="progress-text">{{ user.activity }}%</span>
              </div>
            </td>
            <td>
              <div class="actions">
                <button 
                  class="btn-icon" 
                  @click="$emit('edit-user', user)"
                  title="Редактировать"
                >
                  <i class="fas fa-edit"></i>
                </button>
                <button 
                  class="btn-icon btn-danger" 
                  @click="$emit('delete-user', user)"
                  title="Удалить"
                >
                  <i class="fas fa-trash"></i>
                </button>
                <button 
                  class="btn-icon btn-info" 
                  @click="$emit('view-user', user)"
                  title="Просмотр"
                >
                  <i class="fas fa-eye"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Пагинация -->
    <div class="table-footer">
      <div class="pagination-info">
        Показано {{ startIndex }}-{{ endIndex }} из {{ filteredUsers.length }}
      </div>
      <div class="pagination-controls">
        <button 
          class="btn btn-sm" 
          :disabled="currentPage === 1"
          @click="currentPage--"
        >
          <i class="fas fa-chevron-left"></i>
        </button>
        
        <span class="page-info">
          Страница {{ currentPage }} из {{ totalPages }}
        </span>
        
        <button 
          class="btn btn-sm" 
          :disabled="currentPage === totalPages"
          @click="currentPage++"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'UsersTable',
  props: {
    data: {
      type: Object,
      default: () => ({})
    },
    title: {
      type: String,
      default: 'Пользователи'
    }
  },
  emits: ['add-user', 'edit-user', 'delete-user', 'view-user'],
  setup(props) {
    const currentPage = ref(1)
    const itemsPerPage = ref(5)
    const sortBy = ref('name')
    const sortDirection = ref('asc')

    // Статусы пользователей
    const userStatuses = {
      active: 'Активен',
      inactive: 'Неактивен',
      pending: 'Ожидание',
      blocked: 'Заблокирован'
    }

    // Колонки таблицы
    const columns = ref([
      { key: 'name', title: 'Пользователь', sortable: true },
      { key: 'status', title: 'Статус', sortable: true },
      { key: 'joinDate', title: 'Дата регистрации', sortable: true },
      { key: 'activity', title: 'Активность', sortable: true }
    ])

    // Данные по умолчанию
    const defaultUsers = [
      {
        id: 1,
        name: 'Иван Петров',
        email: 'ivan@example.com',
        avatar: '',
        status: 'active',
        joinDate: '2024-01-15',
        activity: 85
      },
      {
        id: 2,
        name: 'Мария Сидорова',
        email: 'maria@example.com',
        avatar: '',
        status: 'active',
        joinDate: '2024-01-10',
        activity: 92
      },
      {
        id: 3,
        name: 'Алексей Козлов',
        email: 'alexey@example.com',
        avatar: '',
        status: 'inactive',
        joinDate: '2024-01-05',
        activity: 45
      },
      {
        id: 4,
        name: 'Елена Новикова',
        email: 'elena@example.com',
        avatar: '',
        status: 'pending',
        joinDate: '2024-01-20',
        activity: 67
      },
      {
        id: 5,
        name: 'Дмитрий Волков',
        email: 'dmitry@example.com',
        avatar: '',
        status: 'blocked',
        joinDate: '2023-12-15',
        activity: 23
      }
    ]

    const users = ref(props.data.users || defaultUsers)

    // Сортировка и пагинация
    const filteredUsers = computed(() => {
      return [...users.value].sort((a, b) => {
        const aValue = a[sortBy.value]
        const bValue = b[sortBy.value]
        
        if (sortDirection.value === 'asc') {
          return aValue > bValue ? 1 : -1
        } else {
          return aValue < bValue ? 1 : -1
        }
      })
    })

    const totalPages = computed(() => 
      Math.ceil(filteredUsers.value.length / itemsPerPage.value)
    )

    const paginatedUsers = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      const end = start + itemsPerPage.value
      return filteredUsers.value.slice(start, end)
    })

    const startIndex = computed(() => 
      (currentPage.value - 1) * itemsPerPage.value + 1
    )

    const endIndex = computed(() => 
      Math.min(currentPage.value * itemsPerPage.value, filteredUsers.value.length)
    )

    // Методы
    const sortTable = (column) => {
      if (sortBy.value === column) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
      } else {
        sortBy.value = column
        sortDirection.value = 'asc'
      }
      currentPage.value = 1
    }

    const getSortIcon = (column) => {
      if (sortBy.value !== column) return ''
      return sortDirection.value === 'asc' ? 'sort-asc' : 'sort-desc'
    }

    const getUserStatus = (status) => userStatuses[status] || status

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('ru-RU')
    }

    const handleImageError = (event) => {
      event.target.src = '/default-avatar.png'
    }

    const exportUsers = () => {
      console.log('Экспорт пользователей')
    }

    onMounted(() => {
      if (props.data.users) {
        users.value = props.data.users
      }
    })

    return {
      columns,
      currentPage,
      itemsPerPage,
      filteredUsers,
      paginatedUsers,
      totalPages,
      startIndex,
      endIndex,
      sortTable,
      getSortIcon,
      getUserStatus,
      formatDate,
      handleImageError,
      exportUsers
    }
  }
}
</script>

<style scoped>
.users-table {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.table-header h4 {
  margin: 0;
  color: #2d3748;
  font-size: 16px;
  font-weight: 600;
}

.table-actions {
  display: flex;
  gap: 8px;
}

.btn {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  background: white;
  color: #4a5568;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn:hover {
  background: #f7fafc;
}

.btn-primary {
  background: #4299e1;
  color: white;
  border-color: #4299e1;
}

.btn-primary:hover {
  background: #3182ce;
}

.btn-sm {
  padding: 6px 10px;
  font-size: 12px;
}

.table-container {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.column-header {
  font-weight: 600;
  color: #4a5568;
  background: #f7fafc;
}

.column-header.sortable {
  cursor: pointer;
  user-select: none;
}

.column-header.sortable:hover {
  background: #edf2f7;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-icon {
  color: #cbd5e0;
  transition: color 0.2s;
}

.sort-asc .sort-icon,
.sort-desc .sort-icon {
  color: #4299e1;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  background: #e2e8f0;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-name {
  font-weight: 500;
  color: #2d3748;
}

.user-email {
  font-size: 12px;
  color: #718096;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-active {
  background: #c6f6d5;
  color: #276749;
}

.status-inactive {
  background: #fed7d7;
  color: #c53030;
}

.status-pending {
  background: #fefcbf;
  color: #744210;
}

.status-blocked {
  background: #e2e8f0;
  color: #4a5568;
}

.progress-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #48bb78;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 12px;
  color: #718096;
  min-width: 30px;
}

.actions {
  display: flex;
  gap: 4px;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: #718096;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: #f7fafc;
  color: #4a5568;
}

.btn-icon.btn-danger:hover {
  background: #fed7d7;
  color: #c53030;
}

.btn-icon.btn-info:hover {
  background: #bee3f8;
  color: #2c5aa0;
}

.table-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-top: 1px solid #e2e8f0;
  background: #f7fafc;
}

.pagination-info {
  font-size: 14px;
  color: #718096;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-info {
  font-size: 14px;
  color: #4a5568;
}
</style>