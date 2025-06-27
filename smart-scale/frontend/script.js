document.addEventListener('DOMContentLoaded', () => {
    const userIdInput = document.getElementById('userId');
    const fetchDataBtn = document.getElementById('fetchData');
    const measurementsList = document.getElementById('measurementsList');
    const errorMessage = document.getElementById('errorMessage');

    fetchDataBtn.addEventListener('click', async () => {
        const userId = userIdInput.value.trim();
        measurementsList.innerHTML = '';
        errorMessage.textContent = '';

        if (!userId) {
            errorMessage.textContent = 'Proszę wprowadzić ID użytkownika.';
            return;
        }

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/measurements/${userId}`);
            
            if (response.ok) {
                const data = await response.json();
                if (data.length > 0) {
                    data.forEach(measurement => {
                        const measurementDiv = document.createElement('div');
                        measurementDiv.classList.add('measurement-item');
                        measurementDiv.innerHTML = `
                            <p><strong>ID Użytkownika:</strong> ${measurement.user_id}</p>
                            <p><strong>Waga:</strong> ${measurement.weight} kg</p>
                            <p><strong>Procent tłuszczu:</strong> ${measurement.fat_percentage}%</p>
                            <p><strong>Procent wody:</strong> ${measurement.water_percentage}%</p>
                            <p><strong>Data pomiaru:</strong> ${new Date(new Date(measurement.timestamp).getTime() + (2 * 60 * 60 * 1000)).toLocaleString()}</p>
                        `;
                        measurementsList.appendChild(measurementDiv);
                    });
                } else {
                    measurementsList.innerHTML = '<p>Brak pomiarów dla tego użytkownika.</p>';
                }
            } else if (response.status === 404) {
                errorMessage.textContent = 'Nie znaleziono pomiarów dla tego użytkownika.';
            } else {
                errorMessage.textContent = `Błąd serwera: ${response.status} - ${response.statusText}`;
            }
        } catch (error) {
            errorMessage.textContent = `Wystąpił błąd podczas pobierania danych: ${error.message}`;
            console.error('Fetch error:', error);
        }
    });
});
