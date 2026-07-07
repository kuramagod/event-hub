document.addEventListener('DOMContentLoaded', () => {
	const conditionPrice = document.getElementById('conditionPrice'); 
	const priceInput = document.getElementById('priceInput');

	conditionPrice.addEventListener('change', (event) => {
		const selectedValue = event.target.value;
		if (selectedValue == "pay")
		{
			priceInput.classList.remove('hidden');
		} else {
			priceInput.classList.add('hidden');
		}
	});
});