export function formatDate(dateString: string): string {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  const [year, month, day] = dateString.split('-').map(Number);
  const correctDate = new Date(year, month - 1, day);

  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(correctDate);
}