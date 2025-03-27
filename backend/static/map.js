class MapController {
    constructor() {
        this.map = null;
        this.markers = null;
        this.clientesObrasLayer = null;
        this.tecnicosLayer = null;
        this.circlesLayer = null; // Nova camada para os círculos
        this.init();
    }

    init() {
        this.initMap();
        this.initMarkerCluster();
        this.initCirclesLayer(); // Inicializa a camada de círculos
        this.loadTechnicians();
        this.loadKMLLayers();
        this.initEventListeners();
    }

    initMap() {
        this.map = L.map('map', {
            center: [-15.7797, -47.9297],
            zoom: 5,
            zoomControl: true,
            maxZoom: 18,
            minZoom: 3
        });

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18,
            minZoom: 3
        }).addTo(this.map);
    }

    initMarkerCluster() {
        this.markers = L.markerClusterGroup();
    }

    initCirclesLayer() {
        this.circlesLayer = L.layerGroup(); // Cria uma camada para os círculos
    }

    addTechnicianMarker(technician) {
        // Criar círculo e adicionar à camada de círculos
        const circle = L.circle([technician.latitude, technician.longitude], {
            color: 'red',
            fillColor: '#f03',
            fillOpacity: 0.07,
            radius: 300000
        });
        this.circlesLayer.addLayer(circle);

        // Criar marcador e adicionar ao cluster
        const marker = L.marker([technician.latitude, technician.longitude])
            .bindPopup(`<b>${technician.nome}</b><br>${technician.cidade} - ${technician.estado}<br>${technician.empresa}`);
        this.markers.addLayer(marker);
    }

    async loadTechnicians() {
        try {
            const response = await fetch('/tecnicos');
            if (!response.ok) throw new Error('Erro ao carregar técnicos');
            const technicians = await response.json();
            technicians.forEach(tech => this.addTechnicianMarker(tech));
            this.tecnicosLayer = L.layerGroup([this.markers, this.circlesLayer]); // Combina marcadores e círculos
            this.updateLayers();
        } catch (error) {
            console.error('Error:', error);
            alert('Erro ao carregar técnicos.');
        }
    }

    loadKMLLayers() {
        const obrasIcon = L.icon({
            iconUrl: 'https://cdn-icons-png.flaticon.com/512/5690/5690026.png',
            iconSize: [32, 32],
            iconAnchor: [16, 32]
        });

        const clientesLayer = this.loadKML("/static/Clientes.KML", "Cliente", obrasIcon);
        const obrasLayer = this.loadKML("/static/Obras_2024.KML", "Obra", obrasIcon);
        this.clientesObrasLayer = L.layerGroup([clientesLayer, obrasLayer]);
        this.updateLayers();
    }

    loadKML(url, layerName, icon) {
        return omnivore.kml(url)
            .on('ready', function() {
                this.eachLayer(layer => {
                    if (layer.feature.geometry.type === 'Point') {
                        layer.setIcon(icon);
                        layer.bindPopup(`<b>${layerName}:</b> ${layer.feature.properties.name || 'Sem nome'}`);
                    }
                });
            });
    }

    updateLayers() {
        this.map.eachLayer(layer => {
            if (layer instanceof L.TileLayer) return;
            this.map.removeLayer(layer);
        });

        if (document.getElementById('filter-clientes-obras').checked && this.clientesObrasLayer) {
            this.clientesObrasLayer.addTo(this.map);
        }
        if (document.getElementById('filter-tecnicos').checked && this.tecnicosLayer) {
            this.tecnicosLayer.addTo(this.map);
        }
    }

    initEventListeners() {
        document.getElementById('filter-clientes-obras').addEventListener('change', () => this.updateLayers());
        document.getElementById('filter-tecnicos').addEventListener('change', () => this.updateLayers());
    }
}

class UIController {
    constructor() {
        this.activeModal = null;
        this.init();
    }

    init() {
        this.initEventListeners();
    }

    initEventListeners() {
        document.getElementById('toggle-popup').addEventListener('click', () => this.togglePopup());
        document.getElementById('btn-add-tecnico').addEventListener('click', () => this.openAddModal());
        document.getElementById('btn-remove-tecnico').addEventListener('click', () => this.openRemoveModal());
        
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) this.closeModal();
            });
        });

        document.querySelectorAll('[data-action="close"]').forEach(button => {
            button.addEventListener('click', () => this.closeModal());
        });

        document.querySelectorAll('[data-action="remove"]').forEach(button => {
            button.addEventListener('click', () => this.removeTechnician());
        });

        document.getElementById('add-form').addEventListener('submit', (e) => this.handleAddTechnician(e));

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAllModals();
                this.closePopup();
            }
        });
    }

    togglePopup() {
        const popup = document.getElementById('popup');
        popup.style.display = popup.style.display === 'block' ? 'none' : 'block';
    }

    closePopup() {
        document.getElementById('popup').style.display = 'none';
    }

    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            this.activeModal = modal;
            document.body.style.overflow = 'hidden';
        }
    }

    closeModal() {
        if (this.activeModal) {
            this.activeModal.classList.remove('active');
            this.activeModal = null;
            document.body.style.overflow = '';
        }
    }

    closeAllModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.remove('active');
        });
        this.activeModal = null;
        document.body.style.overflow = '';
    }

    async openAddModal() {
        this.closePopup();
        this.openModal('add-modal');
    }

    async openRemoveModal() {
        this.closePopup();
        this.openModal('remove-modal');
        await this.loadTechniciansList();
    }

    async loadTechniciansList() {
        const select = document.getElementById('tecnicos-list');
        select.innerHTML = '';
        try {
            const response = await fetch('/tecnicos');
            if (!response.ok) throw new Error('Erro ao carregar técnicos');
            const technicians = await response.json();
            technicians.forEach(tech => {
                const option = document.createElement('option');
                option.value = tech.id;
                option.textContent = `${tech.nome} - ${tech.cidade} - ${tech.estado} - ${tech.empresa}`;
                select.appendChild(option);
            });
        } catch (error) {
            console.error('Error:', error);
            alert('Erro ao carregar lista de técnicos.');
        }
    }

    async handleAddTechnician(e) {
        e.preventDefault();
        const formData = {
            nome: document.getElementById('nome').value,
            cidade: document.getElementById('cidade').value,
            estado: document.getElementById('estado').value,
            empresa: document.getElementById('empresa').value
        };

        try {
            const response = await fetch('/tecnicos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!response.ok) throw new Error('Erro ao adicionar técnico');
            
            alert('Técnico adicionado com sucesso!');
            this.closeAllModals();
            location.reload();
        } catch (error) {
            console.error('Error:', error);
            alert('Erro ao adicionar técnico.');
        }
    }

    async removeTechnician() {
        const select = document.getElementById('tecnicos-list');
        const id = select.value;
        if (!id) return;

        if (confirm('Tem certeza que deseja remover este técnico?')) {
            try {
                const response = await fetch(`/tecnicos/${id}`, { method: 'DELETE' });
                if (!response.ok) throw new Error('Erro ao remover técnico');
                
                alert('Técnico removido com sucesso!');
                this.closeAllModals();
                location.reload();
            } catch (error) {
                console.error('Error:', error);
                alert('Erro ao remover técnico.');
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const mapController = new MapController();
    const uiController = new UIController();
    window.modalController = uiController;
});